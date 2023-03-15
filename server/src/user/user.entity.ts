import { CoreEntity } from 'src/common/entities/core.entity';
import { Column, Entity, Index } from 'typeorm';

@Entity({ name: 'user' })
export class User extends CoreEntity {
  @Index({ unique: true })
  @Column({ type: 'varchar', length: 255, unique: true })
  email: string;

  @Column({ type: 'varchar', length: 255, select: false })
  password: string;
}
