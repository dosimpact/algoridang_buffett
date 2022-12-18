import {
  CreateDateColumn,
  DeleteDateColumn,
  Entity,
  PrimaryGeneratedColumn,
  UpdateDateColumn,
  VersionColumn,
} from 'typeorm';

@Entity()
export class CoreEntity {
  @PrimaryGeneratedColumn()
  id: number;

  @UpdateDateColumn({ type: 'timestamptz' })
  updateAt: Date;

  @CreateDateColumn({ type: 'timestamptz' })
  createAt: Date;

  @DeleteDateColumn({ type: 'timestamptz' })
  deleteAt: Date;

  @VersionColumn()
  version: number;
}
